import moderngl

ctx = moderngl.create_standalone_context()
buf = ctx.buffer(b'Hello World')
buf.read()


#   faf