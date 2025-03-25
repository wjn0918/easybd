import {Base} from "../base.js"
import axios from 'axios'

class ShingiJZ extends Base {
    constructor(url){
        super(url)
    }

    changeName(params){
        return axios.request(
            {
                url: `${this.url}/process_sheet`,
                method: 'post',
                data: params,
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )
    }

    rollbackConfig(){
        return axios.request(
            {
                url: `${this.url}/rollback_config`,
                method: 'get',
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )
    }
    
   
}

export const ShingiJZApi = new ShingiJZ('/api/shingi/jz/tools')