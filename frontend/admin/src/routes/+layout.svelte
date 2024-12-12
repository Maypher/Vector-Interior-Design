<script lang="ts">
	import '../app.css';
	import { SvelteToast } from '@zerodevx/svelte-toast';
	let { children } = $props();
</script>

<SvelteToast />
{@render children()}
