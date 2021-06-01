from .base import Base
from trustar2.base import fluent
from trustar2.trustar_enums import WorkflowDestinations, ObservableTypes


@fluent
class WorkflowConfig(Base):

    def __init__(self, workflow_type="INDICATOR_PRIORITIZATION"):
        self.workflow_type = workflow_type
        self.workflow_source = []
        self.workflow_destination = []
        self.priority_scores = []
        self.observable_types = []


    def _get_source_config_obj_from_tuple(self, source_config):
        return WorkflowSourceConfig(*source_config)


    def _get_source_config_obj_from_dict(self, source_config):
        enclave_guid = source_config.get("enclave_guid")
        weight = source_config.get("weight")
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

        raise AttributeError("Valid types to create a source config are: WorkflowSourceConfig, tuple, dict")


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

        raise AttributeError("Valid types to create a destination config are: WorkflowDestinationConfig, tuple, dict")


    def _handle_list(self, source_config_list):
        return [self._get_source_config_obj(source) for source in source_config_list]
            

    def set_source_configs(self, source_config):
        """
        """
        if isinstance(source_config, list):
            self.workflow_source += self._handle_list(source_config)

        else: 
            self.workflow_source.append(self._get_source_config_obj(source_config))


    def set_destination_configs(self, destination_config):
        """
        """
        self.workflow_destination.append(self._get_destination_config_obj(destination_config))


    def set_priority_scores(self, priority_scores):
        """
        """
        self.priority_scores += priority_scores

    
    def set_observable_types(self, observable_types):
        """
        """
        if not isinstance(observable_types, list):
            raise AttributeError("'observable_types' should be a list")

        possible_types = set(ObservableTypes.members())
        if set(observable_types) - possible_types:
            raise AttributeError(
                "Observable Types can only be within the following set: {}".format(possible_types)
            )

        self.observable_types += observable_types


    def serialize(self):
        serialized = super(WorkflowConfig, self).serialize()
        workflow_source = serialized.get("workflowSource")
        workflow_destination = serialized.get("workflowDestination")
        serialized.update({"workflowSource": {"enclaveSourceConfig": workflow_source},
                           "workflowDestination": {"enclaveDestinationConfigs": workflow_destination}})
        return serialized



class WorkflowSourceConfig(Base):

    def __init__(self, enclave_guid, weight):
        self._validate_weight(weight)
        self._validate_enclave_guid(enclave_guid)
        self.enclave_guid = enclave_guid
        self.weight = weight


    def _validate_weight(self, weight):
        if weight > 5 or weight < 1:
            raise AttributeError("Workflow source config weights have to be within 1 and 5.")

    
    def _validate_enclave_guid(self, enclave_guid):
        if not isinstance(enclave_guid, str):
            raise AttributeError("Enclave GUID provided must be a string.")



class WorkflowDestinationConfig(Base):

    def __init__(self, enclave_guid, destination_type):
        self._validate_destination_type(destination_type)
        self._validate_enclave_guid(enclave_guid)
        self.enclave_guid = enclave_guid
        self.destination_type = destination_type

    
    def _validate_enclave_guid(self, enclave_guid):
        if not isinstance(enclave_guid, str):
            raise AttributeError("Enclave GUID provided must be a string.")


    def _validate_destination_type(self, destination_type):
        possible_types = list(WorkflowDestinations.members())
        if not destination_type in possible_types:
            raise AttributeError("Destination type must be one of the following: {}".format(possible_types))
