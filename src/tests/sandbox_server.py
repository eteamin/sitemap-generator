

class SandboxServer:

    def index(self):
        return "Hello World!"

    def some_page(self):
        pass

    def some_other_page(self):
        pass

    index.exposed = True
    some_page.exposed = True
    some_other_page.exposed = True
