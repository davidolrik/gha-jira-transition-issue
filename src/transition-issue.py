from jira import JIRA
from pydantic import AnyHttpUrl, BaseSettings, SecretStr


class Settings(BaseSettings):
    class Config:
        env_prefix = "INPUT_"

    JIRA_USERNAME: str
    JIRA_PASSWORD: SecretStr
    JIRA_BASE_URL: AnyHttpUrl

    ISSUE_KEY: str
    ISSUE_STATUS: str


settings = Settings()

jira = JIRA(
    settings.JIRA_BASE_URL,
    auth=(settings.JIRA_USERNAME, settings.JIRA_PASSWORD.get_secret_value()),
)

issue = jira.issue(settings.ISSUE_KEY)
transitions = jira.transitions(issue)
transition_to_id = {t["name"]: t["id"] for t in transitions}

transition_id = transition_to_id[settings.ISSUE_STATUS]
print(f"Transitioning issue {settings.ISSUE_KEY} to {settings.ISSUE_STATUS}")
jira.transition_issue(issue, transition_id)
