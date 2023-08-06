//el error zay el close

const WebSocket = require('ws');
const isReachable = require('is-reachable');

var inGameFlag = false;
let clientNumber = 0;
const clients = new Map();
const clientsIP = new Map();
const clientsUid = new Map();

var json_arr = [{ client: 1, type: 'run', x: 310, y: 380, y_counter: 0 }, { client: 2, type: 'run', x: 360, y: 380, y_counter: 0 }, { client: 3, type: "run", x: 460, y: 380, y_counter: 0 }]
var current_clients_counter = 0
class Client {
    constructor(socket) {
        clientNumber++;
        this.id = clientNumber;
        this.xCoord = 0;
        this.yCoord = 480;
        this.score = 0;
        this.socket = socket;
        this.inGame = false;
        this.firstConnection = false
        this.state = 'run'// in good condition not crashed
        // Add any other properties you need for the client's state

        //this.sendData('Welcome to the WebSocket server');

    }

    sendData(data) {
        this.socket.send(data);
    }
}

const wss = new WebSocket.Server({ port: 8888 });

wss.on('connection', async function connection(ws, request) {
    const reachable  = await isReachable();
    if (reachable ) {
        console.log('************Client is online*****************Client is online**********');
    } else {
        console.log('Client is offline*********Client is offline*************');
    }
    const id = request.headers['uid'];
    console.log("the id found in header**********", id)
    if (current_clients_counter >= 3) {
        ws.send("reufsed conection")
        ws.terminate();
        return
    }
    if (clientsUid.has(request.headers['uid'])) {

        var reconnectingClientId = clientsUid.get(request.headers['uid']).id;
        if (clientsUid.get(request.headers['uid']).inGame || json_arr[reconnectingClientId - 1]['type'] == 'crash') {
            ws.send("reufsed conection")
            ws.terminate();
            return
        }


        console.log("client who is diconnected trying to reconnect")
        current_clients_counter += 1

    }
    console.log('Client connected');


    console.log(" **********************client trying to connect ip***********", request.headers['uid'])
    console.log(" clientsUid", clientsUid.keys())
    //console.log("type of key",  typeof clientsUid.keys()[0] )
    //console.log(" type of header ip after split",  request.headers['uid'] )
    if (!clientsUid.has(request.headers['uid']) && current_clients_counter < 3) {
        console.log(" **********************client not found in clients IPs", request.headers['uid'])
        const client = new Client(ws);
        current_clients_counter += 1
        // new edit 
        client.id = current_clients_counter
        client.inGame = true;
        client.firstConnection = true
        clients.set(ws, client);
        clientsUid.set(request.headers['uid'], client)

    }

    ws.send("welcome to the server")
    //ws.send("ya rab men el server")
    //setInterval(function () { ws.send('Welcome to the WebSocket server TIMER') }, 1000);
    console.log("a client connected")



    ws.on('message', (message) => {
        var decoded_message = message.toString()
        var client = clientsUid.get(request.headers['uid']);
        //mesh beykhosh gowwa el tart ghaleban 3ayez buffer bardo yeb2a ana keda mastafadtesh haga bel websocket 3an el socket el 3adi
        if (decoded_message === 'run') {
            console.log('In the start condition');
            if (client.id === 1) {
                client.xCoord = 310;
                client.y_Coord = 480
                const coordinates = json_arr[0];
                console.log('sending data now')
                const json = JSON.stringify(coordinates);

                // send the JSON data to the server
                client.sendData(json);
                console.log(json)




                if (inGameFlag) {



                    const starting_data = json_arr;
                    const json = JSON.stringify(starting_data);

                    // send the JSON data to the server
                    console.log(`sending for CLIENT ${client.id}`)
                    client.sendData(json);



                }




            } else if (client.id === 2) {
                client.xCoord = 360;
                client.y_Coord = 480
                console.log("sending for client 2")
                const coordinates = json_arr[1]
                const json = JSON.stringify(coordinates);

                client.sendData(json);


                if (inGameFlag) {



                    const starting_data = json_arr;
                    const json = JSON.stringify(starting_data);

                    // send the JSON data to the server
                    console.log(`sending for CLIENT ${client.id}`)
                    client.sendData(json);





                }



            } else if (client.id === 3) {
                client.xCoord = 460;
                client.y_Coord = 480
                const coordinates = json_arr[2];
                const json = JSON.stringify(coordinates);

                // send the JSON data to the server
                client.sendData(json);
                setTimeout(function () {
                    console.log("One millisecond has passed.");
                }, 1); // wait for 1000 milliseconds (1 second)

                if (!inGameFlag) {
                    for (const [socket, client] of clients.entries()) {

                        const starting_data = json_arr;
                        const json = JSON.stringify(starting_data);
                        inGameFlag = true;
                        // send the JSON data to the server
                        console.log(`sending for CLIENT ${client.id}`)
                        client.sendData(json);


                    }

                }
                else {

                    const starting_data = json_arr;
                    const json = JSON.stringify(starting_data);
                    inGameFlag = true;
                    // send the JSON data to the server
                    console.log(`sending for CLIENT ${client.id}`)
                    client.sendData(json);

                }
            }
        }
        else {
            if (decoded_message.length > 0) {
                console.log(`i am expecting a json and got ${decoded_message}`)
                json_arr[client.id - 1] = JSON.parse(message)
                console.log(`client.id: ${client.id}`)
                console.log(json_arr)
                for (const [socket, cliento] of clients.entries()) {
                    const json_2 = JSON.stringify(json_arr[client.id - 1]);
                    if (cliento.id != client.id) {
                        cliento.sendData(json_2);
                        console.log(`json_2 sent to cliento${cliento.id}`, json_2)
                    }
                }
            }
        }
        console.log(`Received data from client ${client.id}:`, decoded_message);
        // Access and update the client's state as needed
        client.data = message;
    });

    ws.on('close', () => {
        const client = clientsUid.get(request.headers['uid']);
        console.log("client who is trying to disconnect have IP and is client no#", clientsUid.get(request.headers['uid']).id)
        client.inGame = false
        // clients.delete(ws);
        current_clients_counter -= 1
        if (current_clients_counter <= 0) {
            inGameFlag = false;
            clientNumber = 0;
            clients.clear()
            clientsUid.clear()
            json_arr = [{ client: 1, type: 'run', x: 310, y: 380, y_counter: 0 }, { client: 2, type: 'run', x: 360, y: 380, y_counter: 0 }, { client: 3, type: "run", x: 460, y: 380, y_counter: 0 }]
        }
        else if (current_clients_counter > 0 && inGameFlag == false) {

            json_arr = [{ client: 1, type: 'run', x: 310, y: 380, y_counter: 0 }, { client: 2, type: 'run', x: 360, y: 380, y_counter: 0 }, { client: 3, type: "run", x: 460, y: 380, y_counter: 0 }]
            clientsUid.delete(request.headers['uid'])
            clients.delete(ws)
            console.log(clientsUid.keys())
        }
        // closing connection with one player 
        if (current_clients_counter > 0 && current_clients_counter <= 3 && inGameFlag == true) {

            json_arr[client.id - 1]["type"] = "crash"
            const json_2 = JSON.stringify(json_arr[client.id - 1]);
            console.log("client who will disconnect", client.id)
            console.log("1 client will disconnect and  json_arr will be", json_arr[client.id - 1])
            console.log("1 client will disconnect and  json_2", json_arr[client.id - 1])
            for (const [socket, cliento] of clientsUid.entries()) {


                if (cliento.id != client.id) {
                    cliento.sendData(json_2);
                    console.log(`json_2 sent to cliento${cliento.id}`, json_2)
                }
            }
        }
        console.log(`Client ${client.id} disconnected`);
    });

    ws.on('error', (err) => {
        const client = clients.get(ws);
        let errorMessage = '';
        if (err.message === 'read ECONNRESET') {
            errorMessage = `Client ${client.id} connection crashed`;
        }



        if (current_clients_counter <= 0) {
            inGameFlag = false;
            clientNumber = 0;
            clients.clear()
            clientsUid.clear()
            json_arr = [{ client: 1, type: 'run', x: 310, y: 380, y_counter: 0 }, { client: 2, type: 'run', x: 360, y: 380, y_counter: 0 }, { client: 3, type: "run", x: 460, y: 380, y_counter: 0 }]
        }
        else if (current_clients_counter > 0 && inGameFlag == false) {

            json_arr = [{ client: 1, type: 'run', x: 310, y: 380, y_counter: 0 }, { client: 2, type: 'run', x: 360, y: 380, y_counter: 0 }, { client: 3, type: "run", x: 460, y: 380, y_counter: 0 }]
            clientsUid.delete(request.headers['uid'])
            clients.delete(ws)
            console.log(clientsUid.keys())
        }
        // closing connection with one player 
        if (current_clients_counter > 0 && current_clients_counter <= 3 && inGameFlag == true) {

            json_arr[client.id - 1]["type"] = "crash"
            const json_2 = JSON.stringify(json_arr[client.id - 1]);
            console.log("client who will disconnect", client.id)
            console.log("1 client will disconnect and  json_arr will be", json_arr[client.id - 1])
            console.log("1 client will disconnect and  json_2", json_arr[client.id - 1])
            for (const [socket, cliento] of clientsUid.entries()) {


                if (cliento.id != client.id) {
                    cliento.sendData(json_2);
                    console.log(`json_2 sent to cliento${cliento.id}`, json_2)
                }
            }
        }
        console.log(`Client ${client.id} disconnected`);






    });
});

console.log('Server listening on port 8888');
