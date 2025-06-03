import {Base} from "./base.js"
import axios from 'axios'

class DBTools extends Base {
    constructor(url){
        super(url)
    }

    getTablesInSheet(params){
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
    processTable(params){
        return axios.request(
            {
                url: `${this.url}/process_table`,
                method: 'post',
                data: params,
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )
    }

    process2json(params){
        return axios.request(
            {
                url: `${this.url}/tojson`,
                method: 'post',
                data: params,
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )
    }

    buildScript(params){
        return axios.request(
            {
                url: `${this.url}/build_script`,
                method: 'post',
                data: params,
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )
    }
    execScript(params){
        return axios.request(
            {
                url: `${this.url}/exec_script`,
                method: 'post',
                data: params,
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )
    }
   
}

export const DBToolsApi = new DBTools('/api/tools/db')