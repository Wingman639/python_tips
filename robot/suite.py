from robot.api import TestSuite
from robot.api import ResultWriter
from robot.reporting.resultwriter import Results

suite = TestSuite('I am Test Suite')

#TODO: import python module
suite.imports.library('lib.py')


test_case = suite.tests.create('Should Activate Skynet', tags=['smoke'])


kw = test_case.keywords.create(assign=['${var}'], name='Set Variable', args=['value in variable'])
kw2 = test_case.keywords.create('log', args=['this is my first robot python case'])

result = suite.run(critical='smoke', dryrun = 'dryrun',output='skynet.xml')
'''
<class 'robot.result.executionresult.Result'>
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', 
'__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 
'_stat_config', '_status_rc', 'configure', 'errors', 'generated_by_robot', 'handle_suite_teardown_failures', 'return_code', 'save', 'source', 'statistics', 'suite', 'visit']
'''

#result = suite.run()

assert result.return_code == 0

# Report and xUnit files can be generated based on the  result object.
ResultWriter(result).write_results(report='report.html', log='log.html')

# Generating log files requires processing the earlier generated output XML.
#ResultWriter('skynet.xml').write_results()


'''
    from robot.api import logger

    def my_keyword(arg):
        logger.debug('Got argument %s.' % arg)
        do_something()
        logger.info('<i>This</i> is a boring example.', html=True)


        @keyword
        def func():
            # ...
'''

results = Results(None, result)
'''
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', 
'__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 
'_js_result', '_prune', '_result', '_settings', '_sources', 'js_result', 'result', 'return_code']
'''
print results.js_result