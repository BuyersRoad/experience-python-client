# $path = '/Users/danielj/Documents/experience-python-client/powerbi/power_bi_integration.py'
# $path  = 'C:/Users/Administrator/Downloads/experience-python-client/powerbi/power_bi_integration.py'
# $working_path = 'C:/Users/Administrator/Downloads/experience-python-client/powerbi'
$script_type = 'Powershell.exe'
$schedule_time = $args[0]
$task_name = $args[1]
$directory_location = $args[2]
$powerbi_script_path = $args[3]
$action = New-ScheduledTaskAction -Execute $script_type -WorkingDirectory $directory_location -Argument $powerbi_script_path
$trigger = New-ScheduledTaskTrigger -Daily -At $schedule_time
Register-ScheduledTask $task_name -Action $action -Trigger $trigger