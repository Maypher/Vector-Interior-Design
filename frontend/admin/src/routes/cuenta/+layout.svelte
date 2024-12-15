<script>
	import { PUBLIC_apiUrl } from '$env/static/public';
	let { children } = $props();
</script>

<div class="min-h-screen bg-gray-500 flex justify-center align-middle items-center">
	{@render children()}
</div>
