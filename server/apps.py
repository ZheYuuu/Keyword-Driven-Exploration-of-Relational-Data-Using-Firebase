from app import create_app,db
app = create_app()

@app.shell_context_processor
def makeShellContext():
    return {'db':db}

@app.cli.command()
def test():
    '''Run the unit tests.'''
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)