#!/usr/bin/env python

import os
import sys
from StringIO import StringIO

import web
from web import form

contents_dir = './contents/'


class index:
    new_file_form = form.Form(
        form.Textbox('filename', description=''),
        form.Button('Submit', type='submit')
    )

    def content_list(self):
        filenames = os.listdir(contents_dir)
        contents = ''

        for fn in filenames:
            contents += '<a href="/contents/%s">%s</a><br />\n' % (fn, fn)

        return contents

    def GET(self):
        contents = self.content_list()

        f = self.new_file_form()

        return render.contents(f, contents)

    def POST(self):
        contents = self.content_list()

        f = self.new_file_form()
        if not f.validates():
            return render.contents(f, contents)

        # Create the file if it doesn't exist.
        filename = f.get('filename').value
        if not os.path.exists(contents_dir + filename):
            open(contents_dir + filename, 'w').close()
            contents = self.content_list()

        # Generate contents again, after creating new file.
        return render.contents(f, contents)


class view_post:
    def prepare_code(self, file_contents):
        code = file_contents.split('\r\n')[1:]
        code.insert(0, 'from txtngin_util import *')
        code = '\n'.join(code)
        return code

    def run_script(self, code):
        result = ''

        buffer = StringIO()
        sys.stdout = buffer

        try:
            exec(code)
        except:
            result = 'Failed to run script!'

        # Restore stdout
        sys.stdout = sys.__stdout__

        if not result:
            result = buffer.getvalue()

        return result

    def GET(self, name):
        # TODO: Read the file line by line in search of any code segments, and
        # run each code segment one by one.

        contents = ''
        try:
            with open(contents_dir + name, 'r') as fh:
                contents = fh.read()
        except:
            pass

        if contents.split('\r\n')[0] == '!py':
            # Read and execute input file as a python script.

            print 'Running script "%s"' % name
            code = self.prepare_code(contents)
            result = self.run_script(code)

            return render.view_post(name, result)

        return render.view_post(name, contents)


class edit_post:
    text_form = form.Form(
        form.Textarea('text', description=''),
        form.Button('Submit', type='submit'),
    )

    def GET(self, name):
        f = self.text_form()

        contents = ''
        try:
            with open(contents_dir + name, 'r') as fh:
                contents = fh.read()
        except:
            pass

        if contents:
            f.get('text').value = contents

        # f.get('text').description = name

        return render.edit_post(f, name)

    def POST(self, name):
        f = self.text_form()
        if not f.validates():
            return render.edit_post(f, name)

        text_data = f.get('text').value
        try:
            with open(contents_dir + name, 'w') as fh:
                fh.write(text_data)
        except:
            print 'Failed to write to file!'

        raise web.seeother('/contents/' + name)


class delete_post:
    # TODO: Implement an "Are you sure?"-prompt.

    def GET(self, name):
        if os.path.exists(contents_dir + name):
            try:
                os.remove(contents_dir + name)
            except:
                print 'Could not delete file:', name
                return False

        raise web.seeother('/')

# Go from most to least specific path.
urls = (
    '/contents/edit/(.+)', 'edit_post',
    '/contents/delete/(.+)', 'delete_post',
    '/contents/(.+)', 'view_post',
    '/', 'index'
)

render = web.template.render('templates/', base='layout')

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
