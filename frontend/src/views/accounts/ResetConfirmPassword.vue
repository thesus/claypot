<template>
    <div>
        <div class="reset-confirm">
            <form @submit.prevent="submit">
                <input type="password" v-model="password_1" :placeholder="$t('reset_password_confirm.password')">
                <input type="password" v-model="password_2" :placeholder="$t('reset_password_confirm.password_again')">
                <button type="submit" class="btn btn-right">{{ $t('reset_password_confirm.reset') }}</button>
            </form>
        </div>
    </div>
</template>


<script>
import { api, endpoints } from '@/api'

export default {
    data: () => {
        return {
            password_1: null,
            password_2: null
        }
    },
    methods: {
        async submit () {
            try {
                await api(
                    endpoints.password_reset_confirm(),
                    {
                         new_password1: this.password_1,
                         new_password2: this.password_2,
                         uid: this.$route.params.uid,
                         token: this.$route.params.token
                    }
                )
            } catch (err) {
                console.log(err)
            }
        }
    }
}
</script>

<style lang="scss" scoped>
@import '@/modules/inputs.scss';
@import '@/modules/small_form.scss';
</style>
