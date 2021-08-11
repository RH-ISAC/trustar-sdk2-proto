from .base import Base
from trustar2.base import fluent, typename
from trustar2.trustar_enums import (
    WorkflowDestinations, 
    ObservableTypes,
    WorkflowEnum
)

MIN_WEIGHT = 1
MAX_WEIGHT = 5

ENCLAVE_GUID = WorkflowEnum.ENCLAVE_GUID.value
DEST_TYPE = WorkflowEnum.DESTINATION_TYPE.value
WORKFLOW_SOURCE = WorkflowEnum.WORKFLOW_SOURCE.value
WORKFLOW_DEST = WorkflowEnum.WORKFLOW_DEST.value
ENCLAVE_SOURCE_CONFIG = WorkflowEnum.ENCLAVE_SOURCE_CONFIG.value
ENCLAVE_DEST_CONFIG = WorkflowEnum.ENCLAVE_DEST_CONFIG.value



@fluent
class WorkflowConfig(Base):

    def __init__(self, workflow_type="INDICATOR_PRIORITIZATION"):
        self.workflow_type = workflow_type
        self.workflow_source = []
        self.workflow_destination = []
        self.priority_scores = []
        self.observable_types = []

    
    def __repr__(self):
        return "{}(type={})".format(typename(self), self.workflow_type)


    def _get_source_config_obj_from_tuple(self, source_config):
        return WorkflowSourceConfig(*source_config)


    def _get_source_config_obj_from_dict(self, source_config):
        enclave_guid = source_config.get("enclave_guid")
        weight = source_config.get(WorkflowEnum.WEIGHT.value)
        if not enclave_guid or not weight:
            raise AttributeError("'enclave_guid' or 'weight' fields were not provided in dict.")

        return WorkflowSourceConfig(enclave_guid, weight)


    def _get_source_config_obj(self, source_config):
        if isinstance(source_config, WorkflowSourceConfig):
            return source_config

        if isinstance(source_config, tuple):
            return self._get_source_config_obj_from_tuple(source_config)

        if isinstance(source_config, dict):
            return self._get_source_config_obj_from_dict(source_config)

        raise AttributeError(
            "Valid types to create a source config are: WorkflowSourceConfig, tuple, dict"
        )


    def _get_destination_config_obj_from_tuple(self, destination_config):
        return WorkflowDestinationConfig(*destination_config)


    def _get_destination_config_obj_from_dict(self, destination_config):
        enclave_guid = destination_config.get("enclave_guid")
        destination_type = destination_config.get("destination_type")
        if not enclave_guid or not destination_type:
            raise AttributeError("'enclave_guid' or 'destination_type' fields were not provided in dict.")

        return WorkflowDestinationConfig(enclave_guid, destination_type)


    def _get_destination_config_obj(self, destination_config):
        if isinstance(destination_config, WorkflowDestinationConfig):
            return destination_config

        if isinstance(destination_config, tuple):
            return self._get_destination_config_obj_from_tuple(destination_config)

        if isinstance(destination_config, dict):
            return self._get_destination_config_obj_from_dict(destination_config)

        raise AttributeError(
            "Valid types to create a destination config are: WorkflowDestinationConfig, tuple, dict"
        )


    def _handle_list(self, source_config_list):
        return [self._get_source_config_obj(source) for source in source_config_list]

    
    def _raise_if_observables_are_not_valid(self, observable_types):
        possible_types = set(ObservableTypes.members())
        if set(observable_types) - possible_types:
            raise AttributeError(
                "Observable Types can only be within the following set: {}".format(possible_types)
            )
            

    def set_source_configs(self, source_config):
        """Sets the source configuration for a workflow config. 

        :param source_config: This can be a single element or a list of one of the following:

            - WorkflowSourceConfig.
            - tuple: With first element an enclave_guid (string) and the second 
              a weight (int between 1 and 5)
            - dict: With 'enclave_guid' and 'weight' fields populated
        """
        if isinstance(source_config, list):
            self.workflow_source.extend(self._handle_list(source_config))

        else: 
            self.workflow_source.append(self._get_source_config_obj(source_config))


    def set_destination_configs(self, destination_config):
        """Sets the destination configuration for a workflow config. 

        :param destination_config: This can be a single element or a list of one of the following:

            - WorkflowDestinationConfig.
            - tuple: With first element an enclave_guid (string) and the second 
              a destination_type (string - QRADAR or ENCLAVE)
            - dict: With 'enclave_guid' and 'destination_type' fields populated
        """
        self.workflow_destination.append(self._get_destination_config_obj(destination_config))


    def set_priority_scores(self, priority_scores):
        """Sets the priority scores for a workflow config. 

        :param priority_scores: has to be a list of strings (BENIGN, LOW, MEDIUM, HIGH).
        """
        self.priority_scores.extend(priority_scores)

    
    def set_observable_types(self, observable_types):
        """Sets the observable types for a workflow config. 

        :param observable_types: has to be a list of strings or enums with valid TruSTAR observable types.
        """
        if not isinstance(observable_types, list):
            raise AttributeError("'observable_types' should be a list")

        self._raise_if_observables_are_not_valid(observable_types)
        self.observable_types.extend(observable_types)


    def serialize(self):
        serialized = super(WorkflowConfig, self).serialize()
        workflow_source = serialized.get(WORKFLOW_SOURCE)
        workflow_destination = serialized.get(WORKFLOW_DEST)
        serialized.update({WORKFLOW_SOURCE: {ENCLAVE_SOURCE_CONFIG: workflow_source},
                           WORKFLOW_DEST: {ENCLAVE_DEST_CONFIG: workflow_destination}})
        return serialized


    @classmethod
    def from_dict(cls, config_dict):
        obj = cls(workflow_type=config_dict.get(WorkflowEnum.TYPE.value))
        source_configs = config_dict.get(WORKFLOW_SOURCE, {}).get(ENCLAVE_SOURCE_CONFIG, [])
        obj.set_source_configs([
            (str(conf.get(ENCLAVE_GUID)), 
             conf.get(WorkflowEnum.WEIGHT.value)) 
            for conf in source_configs
        ])

        dest_config = config_dict.get(WORKFLOW_DEST, {}).get(ENCLAVE_DEST_CONFIG)[0]
        obj.set_destination_configs((str(dest_config.get(ENCLAVE_GUID)), dest_config.get(DEST_TYPE)))
        obj.set_observable_types(config_dict.get(WorkflowEnum.OBSERVABLE_TYPES.value, []))
        obj.set_priority_scores(config_dict.get(WorkflowEnum.PRIORITY_SCORES.value, []))
        return obj



class WorkflowSourceConfig(Base):

    def __init__(self, enclave_guid, weight):
        self._validate_weight(weight)
        self._validate_enclave_guid(enclave_guid)
        self.enclave_guid = enclave_guid
        self.weight = weight

    
    def __repr__(self):
        return "{}(enclave={}, weight={})".format(typename(self), self.enclave_guid, self.weight)


    def _validate_weight(self, weight):
        if weight > MAX_WEIGHT or weight < MIN_WEIGHT:
            raise AttributeError(
                "Workflow source config weights have to be within {} and {}.".format(MIN_WEIGHT, MAX_WEIGHT)
            )

    
    def _validate_enclave_guid(self, enclave_guid):
        if not isinstance(enclave_guid, str):
            raise AttributeError("Enclave GUID provided must be a string.")



class WorkflowDestinationConfig(Base):

    def __init__(self, enclave_guid, destination_type):
        self._validate_destination_type(destination_type)
        self._validate_enclave_guid(enclave_guid)
        self.enclave_guid = enclave_guid
        self.destination_type = destination_type


    def __repr__(self):
        return "{}(enclave={}, destination_type={})".format(typename(self), self.enclave_guid, self.destination_type)

    
    def _validate_enclave_guid(self, enclave_guid):
        if not isinstance(enclave_guid, str):
            raise AttributeError("Enclave GUID provided must be a string.")


    def _validate_destination_type(self, destination_type):
        possible_types = list(WorkflowDestinations.members())
        if not destination_type in possible_types:
            raise AttributeError("Destination type must be one of the following: {}".format(possible_types))
