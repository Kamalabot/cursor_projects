# XSLT Transformation Explanation

## Overview
This XSLT document transforms complex employee data into the Paychex format. Let's break down each major component:

## Namespace Declarations
```xml
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:hr="http://example.com/hr"
    xmlns:payroll="http://example.com/payroll"
    xmlns:bank="http://example.com/bank"
    xmlns:paychex="http://example.com/paychex">
```
- Declares all necessary namespaces used in both source and target XML
- `xsl` namespace for XSLT functionality
- `hr`, `payroll`, `bank` from source XML
- `paychex` for target format

## Root Template
```xml
<xsl:template match="/">
    <paychex:PayrollBatch>
        <paychex:Metadata>
            <!-- ... -->
        </paychex:Metadata>
        <xsl:apply-templates select="//hr:employee"/>
    </paychex:PayrollBatch>
</xsl:template>
```
- Matches the document root
- Creates the main `PayrollBatch` structure
- Includes static metadata (pay period dates)
- Uses `apply-templates` to process all employees

## Employee Template
```xml
<xsl:template match="hr:employee">
    <paychex:Transaction>
        <!-- ... -->
    </paychex:Transaction>
</xsl:template>
```
This template handles individual employee transformations:

1. **Transaction ID Creation**
   - Creates unique transaction IDs using `concat('TXN-', @id)`
   - Example: Employee 101 becomes "TXN-101"

2. **Employee Information**
   - Maps basic employee data:
     - ID from `@id` attribute
     - Full name from `hr:name`
     - Salary with currency attribute

3. **Bank Information Masking**
   - Uses `substring()` to show only last 4 digits
   - Formula: `concat('****', substring(..., string-length(...) - 3))`
   - Example: "123456789" becomes "****6789"

## Key Features
1. **Data Selection**
   - Processes only active employees
   - Maintains required data structure
   - Preserves currency attributes

2. **Data Security**
   - Masks sensitive bank information
   - Removes unnecessary personal details

3. **Formatting**
   - Maintains consistent XML structure
   - Uses proper indentation (`indent="yes"`)
   - Preserves namespace integrity

## Usage
Apply this XSLT to your source XML using any XSLT processor to generate the Paychex-formatted output.

# XSLT Test Scenarios

Here are various test scenarios to validate the XSLT transformation:

## 1. Basic Valid Employee
```xml
<company xmlns:hr="http://example.com/hr" xmlns:bank="http://example.com/bank">
    <hr:employees>
        <hr:employee id="101" status="active">
            <hr:name>John Doe</hr:name>
            <hr:salary currency="USD">80000</hr:salary>
            <bank:details>
                <bank:account number="123456789"/>
            </bank:details>
        </hr:employee>
    </hr:employees>
</company>
```
**Expected Output:**
```xml
<paychex:PayrollBatch xmlns:paychex="http://example.com/paychex">
    <paychex:Metadata>
        <paychex:payPeriodStart>2025-01-01</paychex:payPeriodStart>
        <paychex:payPeriodEnd>2025-01-15</paychex:payPeriodEnd>
    </paychex:Metadata>
    <paychex:Transaction refId="TXN-101">
        <paychex:Employee>
            <paychex:ID>101</paychex:ID>
            <paychex:FullName>John Doe</paychex:FullName>
            <paychex:Salary currency="USD">80000</paychex:Salary>
            <paychex:MaskedBankInfo>****6789</paychex:MaskedBankInfo>
        </paychex:Employee>
    </paychex:Transaction>
</paychex:PayrollBatch>
```

## 2. Multiple Employees
```xml
<company xmlns:hr="http://example.com/hr" xmlns:bank="http://example.com/bank">
    <hr:employees>
        <hr:employee id="101" status="active">
            <hr:name>John Doe</hr:name>
            <hr:salary currency="USD">80000</hr:salary>
            <bank:details>
                <bank:account number="123456789"/>
            </bank:details>
        </hr:employee>
        <hr:employee id="102" status="active">
            <hr:name>Jane Smith</hr:name>
            <hr:salary currency="USD">90000</hr:salary>
            <bank:details>
                <bank:account number="987654321"/>
            </bank:details>
        </hr:employee>
    </hr:employees>
</company>
```

## 3. Different Currency
```xml
<company xmlns:hr="http://example.com/hr" xmlns:bank="http://example.com/bank">
    <hr:employees>
        <hr:employee id="103" status="active">
            <hr:name>Hans Schmidt</hr:name>
            <hr:salary currency="EUR">75000</hr:salary>
            <bank:details>
                <bank:account number="111222333"/>
            </bank:details>
        </hr:employee>
    </hr:employees>
</company>
```

## 4. Short Account Number
```xml
<company xmlns:hr="http://example.com/hr" xmlns:bank="http://example.com/bank">
    <hr:employees>
        <hr:employee id="104" status="active">
            <hr:name>Mary Johnson</hr:name>
            <hr:salary currency="USD">65000</hr:salary>
            <bank:details>
                <bank:account number="1234"/>
            </bank:details>
        </hr:employee>
    </hr:employees>
</company>
```

## 5. Missing Optional Fields
```xml
<company xmlns:hr="http://example.com/hr" xmlns:bank="http://example.com/bank">
    <hr:employees>
        <hr:employee id="105" status="active">
            <hr:name>Bob Wilson</hr:name>
            <hr:salary>70000</hr:salary>
            <bank:details>
                <bank:account number="999888777"/>
            </bank:details>
        </hr:employee>
    </hr:employees>
</company>
```

## 6. Special Characters in Name
```xml
<company xmlns:hr="http://example.com/hr" xmlns:bank="http://example.com/bank">
    <hr:employees>
        <hr:employee id="106" status="active">
            <hr:name>María O'Connor-Smith</hr:name>
            <hr:salary currency="USD">95000</hr:salary>
            <bank:details>
                <bank:account number="444555666"/>
            </bank:details>
        </hr:employee>
    </hr:employees>
</company>
```

## Test Cases Verify:
1. **Basic Transformation**: Correct structure and data mapping
2. **Multiple Records**: Proper handling of multiple employees
3. **Currency Handling**: Different currency codes
4. **Account Masking**: Various account number lengths
5. **Optional Fields**: Missing attributes/elements
6. **Special Characters**: Name fields with special characters
7. **Namespace Handling**: Correct namespace usage in output

Each test case should validate:
- Correct XML structure
- Proper namespace usage
- Data transformation accuracy
- Bank account masking
- Currency attribute preservation
- Transaction ID generation

These test cases help ensure the XSLT handles various scenarios correctly and produces valid output according to the Paychex format specifications.

