import { io, Socket } from "socket.io-client";


let socket: Socket | null = null;

function initOxygen(port: number = 15999) {
  const url = `http://localhost:${port}`;
  socket = io(url);

  if(socket) {
    window.addEventListener("beforeunload", () => socket!.emit("onclose"));
  }
}

function invoke<T>(event: string, data: any): Promise<T> {
  if (!socket) {
    throw new Error("Socket not initialized. Call 'initOxygen' first.");
  }

  return new Promise((resolve, reject) => {
    socket!.emit(event, data, (response: T) => {
      if (response && (response as any).error) {
        reject((response as any).error);
      } else {
        resolve(response);
      }
    });
  });
}

function onEvent(event: string, listener?: any) {
  if (!socket) {
    throw new Error("Socket not initialized. Call 'initOxygen' first.");
  }

  socket.on(event, listener)
}

function offEvent(event: string, listener?: any) {
  if (!socket) {
    throw new Error("Socket not initialized. Call 'initOxygen' first.");
  }

  socket.off(event, listener)
}

export { initOxygen, invoke, onEvent, offEvent };