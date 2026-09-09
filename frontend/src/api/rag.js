import axios from "axios"


const api = axios.create({

    baseURL:"http://127.0.0.1:8000",

    timeout:30000

})


export function getFiles(){

    return api.get("/files")

}



export function uploadFile(file){

    let formData = new FormData()

    formData.append(
        "file",
        file
    )


    return api.post(
        "/parse",
        formData,
        {
            headers:{
                "Content-Type":"multipart/form-data"
            }
        }
    )

}



export function deleteFile(filename){

    return api.delete(
        `/files/${filename}`
    )

}



export function chat(question){

    return api.post(
        "/chat",
        null,
        {
            params:{
                question
            }
        }
    )

}