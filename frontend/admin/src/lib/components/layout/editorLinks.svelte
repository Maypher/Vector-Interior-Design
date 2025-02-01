<script lang="ts">
	const { mobileUrl, desktopUrl }: { mobileUrl: string; desktopUrl: string } = $props();
</script>

<div class="flex gap-5">
	<a
		href={mobileUrl}
		class="border-dashed border-2 border-white p-5 block hover:scale-110 transition-all rounded-lg"
		><span class="material-symbols-outlined" style="font-size: 5rem;"> smartphone </span>
		<p class="block text-center">Móvil</p>
	</a>
	<a
		href={desktopUrl}
		class="border-dashed border-2 border-white block p-5 hover:scale-110 transition-all rounded-lg"
		><span class="material-symbols-outlined" style="font-size: 5rem;"> desktop_windows </span>
		<p class="block text-center">Escritorio</p>
	</a>
</div>
