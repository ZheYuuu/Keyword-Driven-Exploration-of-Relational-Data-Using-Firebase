from app import create_app,db
import click
import os
import sys

app = create_app()
@app.shell_context_processor
def makeShellContext():
    return {'db':db}

cov = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage 
    cov = coverage.coverage(branch=True, include='app/*')
    cov.start()

@app.cli.command()
@click.option('--coverage/--no-coverage', default=False, help='Run tests under code coverage.')
def test(coverage):
    '''Run the unit tests.'''
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import subprocess
        os.environ['FLASK_COVERAGE'] = '1'
        sys.exit(subprocess.call(sys.argv))

    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

    if cov:
        cov.stop()
        cov.save()
        print('Coverage Summary:')
        cov.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(os.path.join(basedir, 'tmp'), 'coverage')
        cov.html_report(directory=covdir)
        print('')
        print('HTML report be stored in: %s'%os.path.join(covdir,'index.html'))
        cov.erase()




