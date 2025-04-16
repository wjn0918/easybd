<<template>
    <div>
        <common-config
        :config-api="configApi" 
        conf-type="hikapi" 
        dialog-title="hikapi"
            />
    </div>
</template>
<script lang="ts" setup>
import CommonConfig from "../CommonConfig.vue";
import { ConfigApi } from "@/api/api.js";

const configApi = ConfigApi
</script>