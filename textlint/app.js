const http = require('http')

const hostname = '0.0.0.0'
const port = 3000

const linter = (text) => {
    // console.log(text)
    const TextLintEngine = require("textlint").TextLintEngine
    const engine = new TextLintEngine()  // Load .textlintrc
    return engine.executeOnText(text)
        .then((results) => {
            // console.log(results[0].messages)
            if (engine.isErrorResults(results)) {  // have error
                const output = engine.formatResults(results)
                // console.log(output)
                return results[0].messages
            } else {  // have no error
                throw Error('TETXLINT_RESULTS_ERROR')
            }
            /* messages are `TextLintMessage` array.
            [
                {
                    id: "rule-name",
                    message:"lint message",
                    line: 1, // 1-based columns(TextLintMessage)
                    column:1 // 1-based columns(TextLintMessage)
                }
            ]
            */
        })
}

const router = (req, res, httpVersion, method, path) => {
    console.log("HTTP/%d %s %s", httpVersion, method, path)

    if (method === "GET" && path === "/") {

        res.writeHead(200, {
            'Content-Type': 'application/json',
        });
        const resBody = {
            "status": "Running"
        }
        res.write(JSON.stringify(resBody))
        res.end()

    } else if (method === "POST" && path === "/textlint") {

        let body = [];
        req.on('error', (err) => {  // Error Handling

            console.error(err)

        }).on('data', (chunk) => {  // Append Payload

            body.push(chunk)
            // console.log(body)

        }).on('end', () => {  // Make Response
            // Concat Body
            body = Buffer.concat(body).toString()
            res.on('error', (err) => {
                console.error(err)
            })

            // Call lint func
            linter(body)
                .then((reviewedText) => {
                    // Create Response
                    res.writeHead(200, {
                        'Content-Type': 'application/json'
                    })
                    res.write(JSON.stringify(reviewedText))
                    res.end()
                })
        })
    }
}

const server = http.createServer((request, response) => {
    const { httpVersion, headers, url, method } = request
    router(request, response, httpVersion, method, url)
})

server.listen(port, hostname, () => {
    console.log(`Server running at http://${hostname}:${port}/`)
})
