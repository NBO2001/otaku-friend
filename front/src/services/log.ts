import api from "./api"


export const addLog = async (log: string) => {

    await api.post("/log", {
        log
    },{
        headers: {
            'Content-Type': 'application/json'
        }
    });

}