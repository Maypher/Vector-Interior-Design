<script lang="ts">
	import { page } from '$app/state';
</script>

<div>
	{page.status}
	{page.error?.message}
</div>
