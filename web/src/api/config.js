import {Base} from "./base.js"
import axios from 'axios'

class Config extends Base {
    constructor(url){
        super(url)
    }


    getConfig(){
        return axios.request(
            {
                url: `${this.url}/select`,
                method: 'get',
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )
    }

    
    getConfigByConfigType(configType){
        return axios.request(
            {
                url: `${this.url}/select/${configType}`,
                method: 'get',
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )
    }

    createConfig(params){
        return axios.request(
            {
                url: `${this.url}/create`,
                method: 'post',
                data: params,
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )
    }

    deleteConfig(id){
        return axios.request(
            {
                url: `${this.url}/${id}`,
                method: 'delete',
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )
    }

    updateConfig(id, params){
        return axios.request(
            {
                url: `${this.url}/update/${id}`,
                method: 'post',
                data: params,
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )
    }
   
}

export const ConfigApi = new Config('/api/config')