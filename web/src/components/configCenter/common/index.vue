<<template>
    <div>
        <common-config
        :config-api="configApi" 
        conf-type="common" 
        dialog-title="特殊配置编辑"
            />
    </div>
</template>
<script lang="ts" setup>
import CommonConfig from "../CommonConfig.vue";
import { ConfigApi } from "@/api/api.js";

const configApi = ConfigApi
</script>