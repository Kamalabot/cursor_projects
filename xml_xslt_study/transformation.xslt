<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:hr="http://example.com/hr"
    xmlns:payroll="http://example.com/payroll"
    xmlns:bank="http://example.com/bank"
    xmlns:paychex="http://example.com/paychex">

    <!-- Output settings -->
    <xsl:output method="xml" indent="yes"/>

    <!-- Root template -->
    <xsl:template match="/">
        <paychex:PayrollBatch>
            <!-- Static Metadata section -->
            <paychex:Metadata>
                <paychex:payPeriodStart>2025-01-01</paychex:payPeriodStart>
                <paychex:payPeriodEnd>2025-01-15</paychex:payPeriodEnd>
            </paychex:Metadata>
            
            <!-- Process each employee -->
            <xsl:apply-templates select="//hr:employee"/>
        </paychex:PayrollBatch>
    </xsl:template>

    <!-- Employee template -->
    <xsl:template match="hr:employee">
        <paychex:Transaction>
            <xsl:attribute name="refId">
                <xsl:value-of select="concat('TXN-', @id)"/>
            </xsl:attribute>
            
            <paychex:Employee>
                <paychex:ID><xsl:value-of select="@id"/></paychex:ID>
                <paychex:FullName><xsl:value-of select="hr:name"/></paychex:FullName>
                <paychex:Salary>
                    <xsl:attribute name="currency">
                        <xsl:value-of select="hr:salary/@currency"/>
                    </xsl:attribute>
                    <xsl:value-of select="hr:salary"/>
                </paychex:Salary>
                <paychex:MaskedBankInfo>
                    <xsl:value-of select="concat('****', substring(bank:details/bank:account/@number, string-length(bank:details/bank:account/@number) - 3))"/>
                </paychex:MaskedBankInfo>
            </paychex:Employee>
        </paychex:Transaction>
    </xsl:template>

</xsl:stylesheet>
