<script lang="ts">
    import { onMount } from 'svelte';
    import { WIKI_BACK_URL } from '$lib/constants';

    let treeData;

    onMount(async () => {
        const response = await fetch(`${WIKI_BACK_URL}/tree`);
        if (response.ok) {
            treeData = await response.json();
            console.log(treeData);
        } else {
            console.error('Failed to fetch tree data');
        }
    });
</script>

<!-- ツリー情報を表示するためのコードを追加 -->

<h2> tree of folders (upto lv 5)</h2>

{#if treeData && treeData.root_node}
    <ul>
        <li>/ (root)</li>
        {#if treeData.root_node.folders}
        <ul>
            {#each treeData.root_node.folders as f1}
                <li>{f1.fullpath}</li>
                {#if f1.folders}
                <ul>
                    {#each f1.folders as f2}
                        <li>{f2.fullpath}</li>
                        {#if f2.folders}
                        <ul>
                            {#each f2.folders as f3}
                                <li>{f3.fullpath}</li>
                                {#if f3.folders}
                                <ul>
                                    {#each f3.folders as f4}
                                        <li>{f4.fullpath}</li>
                                        {#if f4.folders}
                                        <ul>
                                            {#each f4.folders as f5}
                                                <li>{f5.fullpath} ({f5.folders.length})</li>
                                            {/each}
                                        </ul>
                                        {/if}
                                    {/each}
                                </ul>
                                {/if}
                            {/each}
                        </ul>
                        {/if}
                    {/each}
                </ul>
                {/if}
            {/each}
        </ul>
        {/if}
    </ul>
{/if}


<hr/>

<h2>list all folders</h2>

{#if treeData && treeData.all_folders}
    <ul>
        {#each Object.values(treeData.all_folders) as f}
            <li>({f.name} / file: {f.num_files}) - {f.fullpath}</li>
        {/each}
    </ul>
{/if}