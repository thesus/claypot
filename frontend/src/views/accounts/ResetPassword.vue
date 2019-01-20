<template>
    <div>
        <div class="reset">
            <form @submit.prevent="submit">
                <h5>{{ $t('reset_password.heading') }}</h5>
                <input type="email" v-model="email" :placeholder="$t('reset_password.email')">
                <button type="submit" class="btn btn-right">{{ $t('reset_password.reset') }}</button>
            </form>
        </div>
    </div>
</template>

<script>
import { api, endpoints } from '@/api'

export default {
    data: () => {
        return {
            email: null
        }
    },
    methods: {
        async submit () {
            try {
                await api(
                    endpoints.password_reset(),
                    {
                        email: this.email
                    }
                )
                this.$router.push({name: 'home'})
            } catch (err) {
                // TODO: Show that something went wrong.
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
