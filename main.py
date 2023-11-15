from website import create_app

app = create_app()

if __name__ == '__main__':  # This is entry point of our project.if you run main file direct then server run.Press CTRL+C to close the server.
    app.run(debug=True)     # This is a debugging server.Every time changing to any of our python code.
                            # Its going auto rerun the web server.