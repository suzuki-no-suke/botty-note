<script lang="ts">
    import { base } from '$app/paths';
	import '../app.css';
	let { children } = $props();


</script>

<!-- common menu -->
<div>
	<!-- top bar -->
	<div class="border">
		<button>(hamburger)</button>
		<a href="{base}/">Botty Note</a>
		<span>Top Tree page</span>
	</div>

	<!-- left menu -->
	<!-- (WIP) -->
</div>

<!-- contents -->
{@render children()}

<!-- footer / chatting bar -->
<!-- (WIP) -->

