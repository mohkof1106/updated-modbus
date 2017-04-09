import logging
logger = logging.getLogger("live_control")
import os

import paramiko

from modbus_controller.settings import DATABASES, LOGGING
log_path = LOGGING["handlers"]["file"]["filename"]
paramiko.util.log_to_file(log_path)

temp_location = '/home/'

def bash(s):
    logger.debug("executes command %s" % s)
    stdin, stdout = os.popen2(s)
    stdin.close()
    lines = stdout.readlines(); stdout.close()
    output_string = ""
    for line in lines:
        output_string += line
    return s, output_string

def get_ssh_client():
    global ssh_client
    try:
        return ssh_client
    except NameError:
        ssh_client = paramiko.SSHClient()
        ssh_client.load_system_host_keys()
        return ssh_client

def ssh_bash(link, command):
    host, username = link.host, link.user
    client = get_ssh_client()
    msg = "Sends to %s@%s the command %s" % (username, host, command)
    logger.info(msg)
    client.connect(host, username=username)
    stdin, stdout, stderr = client.exec_command(command)
    res, err = stdout.read(), stderr.read()
    stdin.close(), stdout.close(), stderr.close()
    client.close()
    return msg, str(res), str(err)
    
def ssh_push_config_to_pi(link):
    command = get_command_for_pushing_config_to_pi(link)
    return ssh_bash(link, command)
    
def no_paramiko_push_config_to_pi(link):
    local_db_path = DATABASES["default"]["NAME"]
    db_name = os.path.basename(local_db_path)
    distant_temp_path = os.path.join(temp_location, link.user)
    distant_db_path = os.path.join(distant_temp_path, db_name)
    command = "scp " + local_db_path + " "+ link.user + "@" + link.host + ":" + distant_db_path
    logger.info("Execute command %s" % command)
    return bash(command)
    

def get_command_for_pushing_config_to_pi(link):
    settings_db_path = DATABASES["default"]["NAME"]
    db_name = os.path.basename(settings_db_path)
    distant_temp_path = os.path.join(temp_location, link.user)
    intermediary_db_path = os.path.join(distant_temp_path, db_name)
    reverse_port= link.reverse_port
    distant_project_path = link.distant_project_path
    distant_db_path = os.path.join(distant_project_path, db_name)
    scp_port = "-P " + str(reverse_port) + " " if reverse_port else ""
    command = "scp " + scp_port + intermediary_db_path + " " + link.local_user + "@localhost:" + distant_db_path
    logger.debug(command)
    return command

def get_control_command(project_path, plant_name, daemon_option):
    command = "cd " + project_path + ";"
    command += " python manage.py control --plant=" + plant_name + " --daemon=" + daemon_option + ";"
    return command

def control_plant(link, daemon_option):
    host = "localhost" #link.host
    port = link.reverse_port
    command = 'ssh -p ' + str(port) + ' ' + link.local_user + '@'+ host + ' '
    command += '"' + get_control_command(link.distant_project_path, link.plant.label, daemon_option) + '"'
    return ssh_bash(link, command)

def start_plant(link):
    return control_plant(link, "start")

def stop_plant(link):
    return control_plant(link, "stop")

def status_plant(link):
    return control_plant(link, "status")

def restart_plant(link):
    return control_plant(link, "restart")

def sync_plant(link):
    push_to_intermediary = no_paramiko_push_config_to_pi(link)
    push_from_intermediary = ssh_push_config_to_pi(link)
    return push_to_intermediary + push_from_intermediary + ("Don't forget to restart",)