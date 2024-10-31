<script lang="ts">
    export let folder;
    export let selected = "";

    async function clicked(fullpath: string) {
        selected = fullpath;
    }
</script>

{#if folder}

<ul class="list-disc list-inside">
    <li>
        <button
            class="border p-2"
            on:click={() => clicked(folder.fullpath)}>{folder.fullpath}</button>
    </li>
    {#each folder.folders as f}
    <ul class="list-disc list-inside">
        {#if f.folders && f.folders.length > 0}
            <svelte:self folder={f} bind:selected={selected} />
        {:else}
            <li>
                <button
                    class="border p-2"
                    on:click={() => clicked(f.fullpath)}>{f.fullpath}</button>
            </li>
        {/if}
    </ul>
    {/each}
</ul>

{:else}

<ul>
    <li>Folder not bounded</li>
</ul>

{/if}