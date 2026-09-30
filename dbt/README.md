# Retail Analytics dbt Layer

This directory contains the dbt transformation layer for the
Retail Demand Forecasting & Inventory Optimization project.

## Architecture

Raw Data
    ↓
BigQuery
    ↓
dbt Staging Models
    ↓
dbt Marts
    ↓
Streamlit Dashboard

## Source Tables

- inventory_analysis
- model_comparison

## Staging Models

- stg_inventory
- stg_model_comparison

## Mart Models

- inventory_summary

## BigQuery Configuration

BigQuery credentials must be provided through a local dbt profile
and must never be committed to GitHub.

The project can therefore be connected to a BigQuery dataset
without exposing service-account credentials in the repository.