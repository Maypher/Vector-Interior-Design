<script lang="ts">
	import logo from '$lib/images/logo.svg';
	import pencil from '$lib/images/pencil.svg';
	import { getI18n } from '$lib/i18n';

	const i18n = getI18n();
</script>

<div
	class="bg-vector-grey flex h-screen w-screen flex-col items-center justify-center gap-20 overflow-x-clip p-10"
>
	<a href="/" class="transition-transform hover:scale-110">
		<img src={logo} alt="Vector: Interior Design" class="w-64" />
	</a>
	<div class="flex flex-col items-center gap-20 text-center text-xl">
		<p class="relative z-10 md:whitespace-pre-wrap">
			{$i18n.t('conclusionMain')}
		</p>
		<p>
			{$i18n.t('conclusionSecondary')}
			<b class="relative block md:inline">
				{$i18n.t('slogan')}<b class="text-vector-orange ml-1">.</b>

				<img
					src={pencil}
					alt="pencil"
					class="size-70 rotate-20 absolute bottom-3 right-0 origin-bottom translate-x-1/2"
				/>
			</b>
		</p>
	</div>
</div>

<style>
</style>
