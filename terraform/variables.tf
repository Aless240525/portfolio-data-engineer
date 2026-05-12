variable "project_name" {
  type        = string
  default     = "lakehouse"
  description = "Name of the project"
}

variable "environment" {
  type        = string
  default     = "dev"
  description = "Environment (dev, test, prod)"
}

variable "location" {
  type        = string
  default     = "East US 2"
  description = "Azure Region"
}