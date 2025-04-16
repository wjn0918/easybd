<<template>
    <div>
        <upload-excel
            />
            <common-config-show
            :config-api="configApi" 
        conf-type="excel" 
        dialog-title="配置编辑"
            
            />
    </div>
</template>
<script lang="ts" setup>
import UploadExcel from "@c/excel/uploadExcel.vue";
import CommonConfigShow from "../CommonConfigShow.vue";
import { ConfigApi } from "@/api/api.js";

const configApi = ConfigApi

</script>