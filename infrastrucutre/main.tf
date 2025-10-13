# infrastructure/main.tf

# This block configures the Azure provider for Terraform.
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Define a resource group to hold our resources.
resource "azurerm_resource_group" "rg" {
  name     = "insecure-rg"
  location = "East US"
}

# --- INSECURE RESOURCE 1: Network Security Group (NSG) ---
# This NSG allows RDP (port 3389) access from ANYWHERE on the internet.
# This is a major vulnerability, as it exposes a sensitive management port to attackers.
resource "azurerm_network_security_group" "insecure_nsg" {
  name                = "insecure-vm-nsg"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  security_rule {
    name                       = "AllowRDP_From_Internet"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "3389"
    # THIS IS THE VULNERABILITY: "0.0.0.0/0" means "any IP address".
    source_address_prefix      = "0.0.0.0/0"
    destination_address_prefix = "*"
  }
}

# --- INSECURE RESOURCE 2: Storage Account ---
# This storage account is configured to allow public blob access.
# This means if someone puts sensitive data in a blob container, it could be
# publicly accessible without authentication.
resource "azurerm_storage_account" "insecure_storage" {
  name                     = "insecurestorageaccount12345" # Must be globally unique
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  
  # THIS IS THE VULNERABILITY: Allowing public access to blobs.
  allow_nested_items_to_be_public = true
}