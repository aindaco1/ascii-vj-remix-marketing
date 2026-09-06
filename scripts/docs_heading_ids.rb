#!/usr/bin/env ruby
# Use the site's Markdown engine so translated aliases match real Jekyll IDs.
require "json"
require "kramdown"
require "kramdown-parser-gfm"

def heading_ids(element)
  own = element.type == :header ? [element.attr.fetch("id")] : []
  own + element.children.flat_map { |child| heading_ids(child) }
end

result = JSON.parse($stdin.read).map do |markdown|
  document = Kramdown::Document.new(markdown, input: "GFM")
  document.to_html # The converter assigns IDs, including duplicate suffixes.
  heading_ids(document.root)
end
puts JSON.generate(result)
