<script lang="ts">
	import '../app.css';
	import getI18nStore from '$lib/i18n';
	import { setI18n } from '$lib/i18n';

	let { children } = $props();

	setI18n(getI18nStore());
</script>

{@render children()}
