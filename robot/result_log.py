from robot.result.resultbuilder import ExecutionResult

result = ExecutionResult('output.xml')

from robot.api import ResultWriter

ResultWriter(result).write_results(report='report_2.html', log='log_2.html')