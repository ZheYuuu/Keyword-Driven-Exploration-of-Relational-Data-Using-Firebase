from app import create_app,db
app = create_app()

@app.shell_context_processor
def makeShellContext():
    return {'db':db}