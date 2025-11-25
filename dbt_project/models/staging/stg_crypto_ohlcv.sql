with source as (
    select * from {{ source('raw_crypto', 'crypto_ohlcv') }}
),

renamed as (
    select
        symbol,
        date as metric_date,
        open as open_price,
        high as high_price,
        low as low_price,
        close as close_price,
        volume,
        _dlt_load_id
    from source
)

select * from renamed
