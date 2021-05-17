const http = require('http');

const hostname = '127.0.0.1';
const port = 3000;

const router = (req, res, httpVersion, method, path) => {
    console.log("HTTP/%d %s %s", method, path, httpVersion);
    
    if (method === "GET" && path === "/") {

        res.writeHead(200, {
            'Content-Type': 'application/json',
        });
        const resBody = {
            "status": "Running"
        };
        res.write(JSON.stringify(resBody));
        res.end();

    } else if (method === "POST" && path === "/textlint") {

        let body = [];
        req.on('error', (err) => {  // Error Handling

            console.error(err);

        }).on('data', (chunk) => {  // Append Payload

            body.push(chunk);
            console.log(body);

        }).on('end', () => {  // Make Response

            // Concat Body
            body = Buffer.concat(body).toString();
            res.on('error', (err) => {
                console.error(err);
            });

            // todo: textlint 

            // Create Response
            res.writeHead(200, {
                'Content-Type': 'application/json',
            });
            const resBody = {httpVersion, method, path, body};
            res.write(JSON.stringify(resBody));
            res.end();

        });
    }
}

const server = http.createServer((request, response) => {
    const { httpVersion, headers, url, method } = request;
    router(request, response, httpVersion, method, url);
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
