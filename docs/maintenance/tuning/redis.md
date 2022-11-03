# Redis

## Compression

Cache compression can help tame the memory usage of specialised installation configurations and Community Apps that heavily utilize Redis.

Various compression algorithms are supported, with various strengths. Our testing has shown that lzma works best with our use cases. You can read more at [Django-Redis Compression Support](https://github.com/jazzband/django-redis#compression-support)

Add the following lines to `local.py`

```python
import lzma

CACHES = {
    "default": {
        # ...
        "OPTIONS": {
            "COMPRESSOR": "django_redis.compressors.lzma.LzmaCompressor",
        }
    }
}
```
