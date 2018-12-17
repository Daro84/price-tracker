from project.models.alerts.alert import Alert
from project.common.database import Database

Database.initialize()

alerts_to_update = Alert.find_alerts_to_update()

for alert in alerts_to_update:
    alert.check_price()
    alert.send_email_alert()
