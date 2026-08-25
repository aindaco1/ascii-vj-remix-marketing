# frozen_string_literal: true

require "digest"

module Jekyll
  module PerformanceFilters
    def asset_fingerprint(path)
      source = @context.registers[:site].source
      asset = File.join(source, path.to_s.sub(%r{\A/}, ""))
      Digest::SHA256.file(asset).hexdigest[0, 12]
    end

    def inline_scss(path)
      site = @context.registers[:site]
      source_path = File.join(site.source, path.to_s.sub(%r{\A/}, ""))
      source = File.read(source_path).sub(/\A---\s*\n---\s*\n/, "")
      site.find_converter_instance(Jekyll::Converters::Scss).convert(source)
    end
  end
end

Liquid::Template.register_filter(Jekyll::PerformanceFilters)
