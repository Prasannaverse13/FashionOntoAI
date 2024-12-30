// Fashion ontology tree visualization
let treeData = {
    name: "Fashion",
    children: [
        {
            name: "Apparel",
            children: []
        }
    ]
};

let svg, g;
let zoom;

// Initialize the visualization
document.addEventListener('DOMContentLoaded', function() {
    // Set up the visualization dimensions
    const container = document.getElementById('ontologyContainer');
    const margin = {top: 20, right: 90, bottom: 30, left: 90};
    const width = container.clientWidth - margin.left - margin.right;
    const height = container.clientHeight - margin.top - margin.bottom;

    // Create the SVG container
    svg = d3.select('#ontologyTree')
        .append('svg')
        .attr('width', '100%')
        .attr('height', '100%')
        .attr('viewBox', `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`);

    // Add zoom behavior
    zoom = d3.zoom()
        .scaleExtent([0.5, 2])
        .on('zoom', (event) => {
            g.attr('transform', event.transform);
        });

    svg.call(zoom);

    // Create a group for the tree
    g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Define the tree layout
    const treemap = d3.tree().size([height, width]);

    // Create the tree hierarchy
    updateTree(treeData);

    function updateTree(data) {
        // Creates hierarchy
        const root = d3.hierarchy(data);
        
        // Assigns the data to a hierarchy using parent-child relationships
        const nodes = treemap(root);
    
        // Add links between nodes
        const link = g.selectAll('.link')
            .data(root.links())
            .join('path')
            .attr('class', 'link')
            .attr('fill', 'none')
            .attr('stroke', 'var(--bs-gray-500)')
            .attr('stroke-width', 2)
            .attr('d', d3.linkHorizontal()
                .x(d => d.y)
                .y(d => d.x));
    
        // Add nodes
        const node = g.selectAll('.node')
            .data(root.descendants())
            .join('g')
            .attr('class', 'node')
            .attr('transform', d => `translate(${d.y},${d.x})`);
    
        // Add circles for nodes
        node.selectAll('circle')
            .data(d => [d])
            .join('circle')
            .attr('r', 8)
            .style('fill', 'var(--bs-primary)')
            .style('stroke', 'var(--bs-body-bg)')
            .style('stroke-width', 2);
    
        // Add labels for nodes
        node.selectAll('text')
            .data(d => [d])
            .join('text')
            .attr('dy', '.35em')
            .attr('x', d => d.children ? -13 : 13)
            .attr('text-anchor', d => d.children ? 'end' : 'start')
            .style('fill', 'var(--bs-body-color)')
            .style('font-weight', '500')
            .style('font-size', '12px')
            .text(d => d.data.name);
    }

    // Make updateTree available globally
    window.updateTree = updateTree;
});

// Zoom controls
function zoomIn() {
    svg.transition()
        .duration(300)
        .call(zoom.scaleBy, 1.2);
}

function zoomOut() {
    svg.transition()
        .duration(300)
        .call(zoom.scaleBy, 0.8);
}

// Add new category to the tree
function addCategory() {
    const select = document.getElementById('categorySelect');
    const category = select.value;
    
    if (!category) {
        appUtils.showError('Please select a category');
        return;
    }

    // Add subcategories based on selection
    const subcategories = getSubcategories(category);
    
    // Find the Apparel node
    const apparelNode = treeData.children.find(child => child.name === "Apparel");
    
    // Add new category with subcategories
    apparelNode.children = apparelNode.children || [];
    apparelNode.children.push({
        name: category.charAt(0).toUpperCase() + category.slice(1),
        children: subcategories
    });

    // Update the visualization
    updateTree(treeData);
    
    // Reset selection
    select.value = '';
}

// Get subcategories for each main category
function getSubcategories(category) {
    const subcategoriesMap = {
        'shoe': [
            { name: 'Sneakers' },
            { name: 'Formal Shoes' },
            { name: 'Boots' }
        ],
        'shirt': [
            { name: 'Full Sleeve' },
            { name: 'Half Sleeve' },
            { name: 'Casual' }
        ],
        'pants': [
            { name: 'Jeans' },
            { name: 'Formal' },
            { name: 'Casual' }
        ],
        'dress': [
            { name: 'Formal' },
            { name: 'Casual' },
            { name: 'Party' }
        ]
    };
    
    return subcategoriesMap[category] || [];
}
