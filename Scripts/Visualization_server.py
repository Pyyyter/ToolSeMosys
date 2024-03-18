from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer

def visualization_Server():
    class MyHandler(SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.path = '/index.html'
            return SimpleHTTPRequestHandler.do_GET(self)

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Plotagem dos resultados - UFF</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                text-align: center;
                margin: 40px;
                background-color: #00274c; /* Azul UFF */
                color: #fff; /* Texto branco */
            }

            h1 {
                color: #ffcc29; /* Amarelo UFF */
            }

            .image-container {
                display: flex;
                justify-content: space-around;
                flex-wrap: wrap;
            }

            img {
                margin: 20px;
                border: 2px solid #ffcc29; /* Amarelo UFF */
                border-radius: 20px;
                box-shadow: 0 100px 200px rgba(0, 0, 0, 0.1);
                width: 600px; /* Aumentando a largura das imagens */
            }

            footer {
                margin-top: 40px;
                font-size: 16px;
                color: #ddd; /* Cinza claro */
            }
        </style>
    </head>
    <body>
        <h1>Plotagem dos resultados: Modelo OSeMOSYS</h1>
        <div class="image-container">
            <img src="Plotagem/BC_Landuse.png" alt="Imagem 1" width="400">
            <img src="Plotagem/Emission by Sector.png" alt="Imagem 2" width="400">
            <img src="Plotagem/Emission.png" alt="Imagem 3" width="400">
            <img src="Plotagem/Generation.png" alt="Imagem 4" width="400">
            <img src="Plotagem/New Capacity.png" alt="Imagem 5" width="400">
            <img src="Plotagem/Total Capacity.png" alt="Imagem 6" width="400">
        </div>
        <footer>
            <p>Apresentado por Ramon, Pedro e Gabriel</p>
            <p>&copy; 2024, UFF Plotagem Inc.</p>
        </footer>
    </body>
    </html>
    """
    with open('index.html', 'w') as html_file:
        html_file.write(html_content)

    port = 8080
    handler = MyHandler
    httpd = TCPServer(("", port), handler)

    print(f"Servidor rodando na porta {port}")
    httpd.serve_forever()