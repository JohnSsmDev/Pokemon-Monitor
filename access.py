vip_users = set()
alerts = []

def activate_vip(user_id):
    vip_users.add(user_id)

def is_vip(user_id):
    return user_id in vip_users

def add_alert(alert):
    alerts.append(alert)

def get_alerts():
    return alerts