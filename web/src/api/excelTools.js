import {Base} from "./base.js"
import axios from 'axios'

class ExcelTools extends Base {
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

    processTable2Datax(params){
        return axios.request(
            {
                url: `${this.url}/datax/process_table`,
                method: 'post',
                data: params,
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )
    }


    getDataxTypes(){
        return axios.request(
            {
                url: `${this.url}/datax/get_datax_type`,
                method: 'get',
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

    saveScript(params){
        return axios.request(
            {
                url: `${this.url}/save_script`,
                method: 'post',
                data: params,
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )
    }

    saveScript2Dolphin(params){
        return axios.request(
            {
                url: `/api/dolphinscheduler/resource/online_create`,
                method: 'post',
                data: params,
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )
    }

    readLocalFile(params){
        return axios.request(
            {
                url: `${this.url}/read_local_file`,
                method: 'post',
                data: params,
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )
    }
   
}

export const ExcelApi = new ExcelTools('/api/tools/excel')