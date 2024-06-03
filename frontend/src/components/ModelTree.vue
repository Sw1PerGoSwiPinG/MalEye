<template>
  <div ref="modelTree"></div>
</template>

<script>
import * as d3 from 'd3';

export default {
  mounted() {
    const data = {
      name: 'MaskedAutoencoder',
      children: [
        {
          name: 'patch_embed',
          children: [
            {
              name: 'proj: Conv2d(1\n192\nkernel_size=(2, 2)\nstride=(2, 2))'
            }
          ]
        },
        {
          name: 'blocks',
          children: this.createBlockItems(4, 192, 768)
        },
        {
          name: 'norm: LayerNorm((192,)\neps=1e-06\nelementwise_affine=True)'
        },
        {
          name: 'decoder_embed: Linear(in_features=192\nout_features=128\nbias=True)'
        },
        {
          name: 'decoder_blocks',
          children: this.createBlockItems(2, 128, 512)
        },
        {
          name: 'decoder_norm: LayerNorm((128,)\neps=1e-06\nelementwise_affine=True)'
        },
        {
          name: 'decoder_pred: Linear(in_features=128\nout_features=4\nbias=True)'
        }
      ]
    };

    const width = 2000;
    const height = 600;
    const svg = d3.select(this.$refs.modelTree)
      .append('svg')
      .attr('width', width)
      .attr('height', height);

    const root = d3.hierarchy(data);
    const treeLayout = d3.tree().size([width, height - 100]);
    treeLayout(root);

    svg.selectAll('line')
      .data(root.links())
      .enter()
      .append('line')
      .attr('x1', d => d.source.x)
      .attr('y1', d => d.source.y)
      .attr('x2', d => d.target.x)
      .attr('y2', d => d.target.y)
      .attr('stroke', 'black');

    svg.selectAll('circle')
      .data(root.descendants())
      .enter()
      .append('circle')
      .attr('cx', d => d.x)
      .attr('cy', d => d.y)
      .attr('r', 5)
      .attr('fill', 'blue');

    svg.selectAll('pre')
      .data(root.descendants())
      .enter()
      .append('pre')
      .attr('x', d => d.x)
      .attr('y', d => d.y - 10)
      .attr('text-anchor', 'middle')
      .text(d => d.data.name);
  },
  methods: {
    createBlockItems(count, inFeatures, mlpOutFeatures) {
      const items = [];
      for (let i = 0; i < count; i++) {
        items.push({
          name: `Block ${i + 1}`,
          children: [
            {
              name: `norm1: LayerNorm((${inFeatures},)\neps=1e-06\nelementwise_affine=True)`
            },
            {
              name: 'attn: Attention',
              children: [
                {
                  name: `qkv: Linear(in_features=${inFeatures}\nout_features=${inFeatures * 3}\nbias=True)`
                },
                {
                  name: 'attn_drop: Dropout(p=0.0\ninplace=False)'
                },
                {
                  name: `proj: Linear(in_features=${inFeatures}\nout_features=${inFeatures}\nbias=True)`
                },
                {
                  name: 'proj_drop: Dropout(p=0.0\ninplace=False)'
                }
              ]
            },
            {
              name: 'drop_path: Identity()'
            },
            {
              name: `norm2: LayerNorm((${inFeatures},)\neps=1e-06\nelementwise_affine=True)`
            },
            {
              name: 'mlp: Mlp',
              children: [
                {
                  name: `fc1: Linear(in_features=${inFeatures}\nout_features=${mlpOutFeatures},\nbias=True)`
                },
                {
                  name: 'act: GELU(approximate=\'none\')'
                },
                {
                  name: `fc2: Linear(in_features=${mlpOutFeatures}\nout_features=${inFeatures}\nbias=True)`
                },
                {
                  name: 'drop: Dropout(p=0.0\ninplace=False)'
                }
              ]
            }
          ]
        });
      }
      return items;
    }
  }
};
</script>

<style>
pre {
  white-space: pre-line;
}
</style>