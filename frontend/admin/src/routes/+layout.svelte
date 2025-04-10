<script lang="ts">
	import '../app.css';
	import '$lib/styles/confirmDialog.css';
	import { SvelteToast } from '@zerodevx/svelte-toast';
	let { children } = $props();
</script>

<SvelteToast />
{@render children()}
