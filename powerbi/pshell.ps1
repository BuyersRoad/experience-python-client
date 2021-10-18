$path = '/Users/danielj/Documents/experience-python-client/powerbi/power_bi_integration.py'
$script_type = 'Powershell.exe'
$schedule_time = $args[0]
$task_name = $args[1]
$action = New-ScheduledTaskAction -Execute $script_type -Argument $path
$trigger = New-ScheduledTaskTrigger -Daily -At $schedule_time
Register-ScheduledTask $task_name -Action $action -Trigger $trigger