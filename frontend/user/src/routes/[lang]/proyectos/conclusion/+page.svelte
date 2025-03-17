<script lang="ts">
	import Head from '$lib/components/Head.svelte';
	import { websiteUrl } from '$lib/utilities/constants';
	import logo from '$lib/images/logo.svg';
	import { getI18n } from '$lib/i18n';
	import { page } from '$app/state';
	import symbol from '$lib/images/symbol.svg';
	import whiteLogo from '$lib/images/logo white.svg';
	import mdToHtml from '$lib/utilities/markdown';

	const i18n = getI18n();
</script>

<Head
	title={$i18n.language === 'es' ? 'Conclusión' : 'Conclusion'}
	description={$i18n.t('conclusionBody')}
	url={page.url.toString()}
	alternateEn={`${websiteUrl}/en/proyectos/conclusion`}
	alternateEs={`${websiteUrl}/es/proyectos/conclusion`}
	ogTitle={$i18n.language === 'es' ? 'Conclusión' : 'Conclusion'}
	ogDescription={$i18n.t('conclusionBody')}
	imageUrl={logo}
/>

<div class="header-screen bg-vector-grey relative flex items-center justify-center overflow-clip">
	<div class="-translate-y-1/6 absolute left-1/4 top-0 flex flex-col items-center">
		<img src={symbol} alt="V" id="symbol" />
		<div class="bg-vector-orange relative -top-10 h-screen w-px"></div>
	</div>
	<div
		class="font-Nexa w-9/10 relative top-10 flex h-full flex-col items-center justify-center gap-y-10 lg:h-fit lg:w-full lg:flex-row lg:justify-evenly"
	>
		<span
			class="text-vector-cream -top-[4ch] self-start text-4xl font-thin italic leading-10 lg:relative lg:justify-self-start [&_br]:hidden"
			id="slogan"
		>
			{@html mdToHtml($i18n.t('slogan'))}
		</span>
		<p class="text-vector-cream text-justify brightness-50 lg:basis-1/3 [&_strong]:text-white">
			{@html mdToHtml($i18n.t('conclusionBody'))}
		</p>
		<img src={whiteLogo} alt="Vector: Interior Design" class="h-10" />
		<div class="bg-vector-orange -bottom-30 absolute right-10 h-2 w-8"></div>
	</div>
</div>

<style global>
	:global {
		#slogan p {
			display: flex;
			flex-direction: column;
		}

		#slogan p strong:nth-of-type(2) {
			align-self: end;
			position: relative;
			left: 2ch;
		}
		#slogan p strong:last-of-type {
			position: relative;
			left: 1ch;
		}
	}
</style>
