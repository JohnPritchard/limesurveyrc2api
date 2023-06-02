from collections import OrderedDict
from limesurveyrc2api.exceptions import LimeSurveyError


class _Token(object):

    def __init__(self, api):
        self.api = api

    def add_participants(
            self, survey_id, participant_data, create_token_key=True):
        """
        Add participants to the specified survey.

        Parameters
        :param survey_id: ID of survey to delete participants from.
        :type survey_id: Integer
        :param participant_data: List of participant detail dictionaries.
        :type participant_data: List[Dict]
        :param create_token_key: If True, generate the new token instead of
          using a provided value.
        :type create_token_key: Bool
        """
        method = "add_participants"
        params = OrderedDict([
            ("sSessionKey", self.api.session_key),
            ("iSurveyID", survey_id),
            ("aParticipantData", participant_data),
            ("bCreateToken", create_token_key)
        ])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Error: Invalid survey ID",
                "No token table",
                "No permission"
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is list
        return response

    def add_response(
            self, survey_id, response_data
        ) :
        """
        Returns the id of the inserted survey response.

        Parameters
        :param survey_id: ID of survey to delete participants from.
        :type survey_id: Integer
        :param participant_data: List of participant detail dictionaries.
        :type participant_data: List[Dict]
        :param response_data: The actual response
        :type response_data: Array
        """
        method = "add_response"
        params = OrderedDict([
            ("sSessionKey", self.api.session_key),
            ("iSurveyID", survey_id),
            ("aResponseData", response_data),
        ])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Error: Invalid survey ID",
                "No token table",
                "No permission"
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is str
        return response

    def delete_participants(self, survey_id, token_ids):
        """
        Delete participants (by token) from the specified survey.

        Parameters
        :param survey_id: ID of survey to delete participants from.
        :type survey_id: Integer
        :param token_ids: List of token IDs for participants to delete.
        :type token_ids: List[Integer]
        """
        method = "delete_participants"
        params = OrderedDict([
            ("sSessionKey", self.api.session_key),
            ("iSurveyID", survey_id),
            ("aTokenIDs", token_ids)
        ])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Error: Invalid survey ID",
                "Error: No token table",
                "No permission",
                "Invalid Session Key"
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is dict
        return response

    def get_participant_properties(
            self, survey_id, token_id, token_query_properties=None,
            token_properties=None):
        """
        Get participant properties (by token) from the specified survey.

        Provide either token_id or token_query_dict, not both.

        For token properties for querying and return, choose from:

        ["blacklisted", "completed", "email", "emailstatus", "firstname",
         "language", "lastname", "mpid", "participant_id", "remindercount",
         "remindersent", "sent", "tid", "token", "usesleft", "validfrom",
         "validuntil"]

        Parameters
        :param survey_id: ID of survey to get participant properties for.
        :type survey_id: Integer
        :param token_id: ID of participant to get properties for.
        :type token_id: Integer
        :param token_query_properties: Key(s) / value(s) to use for finding the
          participant among all those that are in the survey.
        :type token_query_properties: Dict[String, Any]
        :param token_properties: Keys to return from RPC call.
        :type token_properties: List[String]
        """
        method = "get_participant_properties"
        if token_id is not None and token_query_properties is not None:
            raise ValueError(
                "Provide either token_id or token_query_dict, not both.")
        if token_query_properties is None:
            token_query_properties = {"tid": token_id}
        token_properties = token_properties or []

        params = OrderedDict([
            ("sSessionKey", self.api.session_key),
            ("iSurveyID", survey_id),
            ("aTokenQueryProperties", token_query_properties),
            ("aTokenProperties", token_properties)
        ])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Error: Invalid survey ID",
                "Error: No token table",
                "Error: No results were found based on your attributes.",
                "Error: More than 1 result was found based on your attributes.",
                "Error: Invalid tokenid",
                "No valid Data",
                "No permission",
                "Invalid Session Key"
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is dict
        return response

    def get_response_ids(self, survey_id,
                       token):
        """
        Return a list of questions from the specified survey.

        Parameters
        :param survey_id: ID of survey to list questions from.
        :type survey_id: Integer
        :param token: 
        :type token: String
        """
        method = "get_response_ids"
        params = OrderedDict([
            ("sSessionKey", self.api.session_key),
            ("iSurveyID", survey_id),
            ("sToken", token)
        ])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Error: Invalid survey ID",
                "Error: Invalid language",
                "Error: IMissmatch in surveyid and groupid",
                "No questions found",
                "No permission",
                "Invalid session key"
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is list
        return response

    def get_summary(self, survey_id, stat_name="all"):
        """
        Get participant properties of a survey.

        For stat name for return, choose from:

        ["token_count", "token_invalid", "token_sent", "token_opted_out",
         "token_completed", "completed_responses", "incomplete_responses",
         "full_responses"]

        Parameters
        :param survey_id: ID of survey
        :type survey_id: Integer
        :param stat_name: Key to return from RPC call, or "all" for everything.
        :type stat_name: String

        :return: dict with keys "token_count", "token_invalid", "token_sent",
            "token_opted_out", and "token_completed" with strings as values.
        """
        method = "get_summary"
        params = OrderedDict([
            ("sSessionKey", self.api.session_key),
            ("iSurveyID", survey_id),
            ("sStatName", stat_name)
        ])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Invalid surveyid",
                "Invalid summary key",
                "No available data",
                "No permission",
                "Invalid session key"
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is dict
        return response

    def invite_participants(self, survey_id, token_ids, uninvited_only=True):
        """
        Send invitation emails for the specified survey participants.

        Parameters
        :param survey_id: ID of survey to invite participants from.
        :type survey_id: Integer
        :param token_ids: List of token IDs for participants to invite.
        :type token_ids: List[Integer]
        :param uninvited_only: If True, only send emails for participants that
          have not been invited. If False, send an invite even if already sent.
        :type uninvited_only: Bool
        """
        method = "invite_participants"
        params = OrderedDict([
            ("sSessionKey", self.api.session_key),
            ("iSurveyID", survey_id),
            ("aTokenIDs", token_ids),
            ("bEmail", uninvited_only)
        ])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Invalid session key",
                "Error: Invalid survey ID",
                "Error: No token table",
                "Error: No candidate tokens",
                "No permission",
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is dict
        return response

    def list_participants(
            self, survey_id, start=0, limit=1000, ignore_token_used=False,
            attributes=False, conditions=None):
        """
        List participants in a survey.

        Parameters
        :param survey_id: ID of survey to invite participants from.
        :type survey_id: Integer
        :param start: Index of first token to retrieve.
        :type start: Integer
        :param limit: Number of tokens to retrieve.
        :type limit: Integer
        :param ignore_token_used: If True, tokens that have been used are not
          returned.
        :type ignore_token_used: Integer
        :param attributes: The extended attributes to include in the response.
        :type attributes: List[String]
        :param conditions: Key(s) / value(s) to use for finding the
          participant among all those that are in the survey.
        :type conditions: List[Dict]
        """
        method = "list_participants"
        conditions = conditions or []
        params = OrderedDict([
            ("sSessionKey", self.api.session_key),
            ("iSurveyID", survey_id),
            ("iStart", start),
            ("iLimit", limit),
            ("bUnused", ignore_token_used),
            ("aAttributes", attributes),
            ("aConditions", conditions)
        ])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Error: Invalid survey ID",
                "Error: No token table",
                "No survey participants found.",
                "Invalid session key",
                "No permission",
                "Invalid Session Key"
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is list
        return response

    def remind_participants(self):
        # TODO
        raise NotImplementedError

    def set_participant_properties(
            self, survey_id,
            token_query_properties,
            token_data,
        ):
        """
        Allow to set properties about a specific participant, only one particpant can be updated.

        Parameters
        :param survey_id: ID of survey to invite participants from.
        :type survey_id: Integer
        :param token_query_properties: List[Dict] of participant properties used to query the participant, or the token id as an integer
        :type token_query_properties: List[Dict]|Integer
        :param token_data: Data to change
        :type token_data: List[Dict]
        """
        method = "set_participant_properties"
        params = OrderedDict([
            ("sSessionKey", self.api.session_key),
            ("iSurveyID", survey_id),
            ("aTokenQueryProperties", token_query_properties),
            ("aTokenData", token_data),
        ])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Error: Invalid survey ID",
                "Error: No token table",
                "Error: Invalid tokenid",
                "No survey participants found.",
                "Invalid session key",
                "No permission",
                "Invalid Session Key",
                "No valid Data",
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is dict
        return response

    def set_question_properties(
            self, survey_id,
            question_id,
            question_data,
            Language = None,
        ):
        """
        List participants in a survey.

        Parameters
        :param survey_id: ID of survey to invite participants from.
        :type survey_id: Integer
        :param question_id: 
        :type question_id: Integer
        :param question_data: 
        :type question_data: List[Dict]
        """
        method = "update_response"
        params = OrderedDict([
            ("sSessionKey", self.api.session_key),
            ("iSurveyID", survey_id),
            ("iQuestionID", question_id),
            ("aQuestionData", question_data),
        ])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Error: Invalid survey ID",
                "Error: No token table",
                "No survey participants found.",
                "Invalid session key",
                "No permission",
                "Invalid Session Key"
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is list
        return response
